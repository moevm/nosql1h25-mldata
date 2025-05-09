"""
Содержит контроллеры приложения. Контроллер является связным звеном между запросами с клиента и бизнес-логикой.
"""
import os
from pathlib import PosixPath, Path

from flask import render_template, Request, Response, current_app, make_response, jsonify, flash, redirect, url_for
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from src.models.FilterValues import FilterValues
from src.models.Dataset import Dataset
from src.models.DatasetFormValues import DatasetFormValues
from src.services.dataset_service import DatasetService


class DatasetController:
    """
    Класс-контроллер для запросов, связанных с датасетами.
    """
    @staticmethod
    def update_dataset(dataset_id: str, form_values: DatasetFormValues, editor_username: str, filepath: str) -> None:
        old_dataset: Dataset = DatasetRepository.get_dataset(dataset_id)

        dataset: Dataset = Dataset.from_form_values(form_values, old_dataset.dataset_id, old_dataset.dataset_author,
                                                    filepath)
        
        if not form_values.dataset_data:
            dataset.dataset_columns = old_dataset.dataset_columns
            dataset.dataset_rows = old_dataset.dataset_rows
            dataset.dataset_size = old_dataset.dataset_size

        dataset.dataset_creation_date = old_dataset.dataset_creation_date
        dataset.dataset_version = old_dataset.dataset_version + 1
        dataset.dataset_last_editor = editor_username

        DatasetRepository.edit_dataset(dataset)

    @staticmethod
    def render_all_datasets() -> str:
        """
        Обращается к методу сервиса для получения списка Brief'ов всех датасетов в БД.
        Отображает страницу с полученными датасетами.
        """
        all_datasets_brief = DatasetService.get_all_datasets_brief()
        return render_template('all_datasets.html', datasets_brief=all_datasets_brief)

    @staticmethod
    def filter_datasets(request: Request) -> Response:
        """
        Обращается к методу сервиса для получения списка Brief'ов датасетов, которые прошли фильтрацию.
        """

        filters: FilterValues = DatasetService.extract_filter_values(request)
        filtered_briefs: list = DatasetService.get_filtered_briefs(filters)

        response: Response = make_response(jsonify([brief.to_dict() for brief in filtered_briefs]), 200)
        return response

    @staticmethod
    def add_dataset(request: Request) -> Response:
        """
        Создается объект DatasetFormData из данных request'а.
        Обращается к методу сервиса для добавления датасета в БД.
        Сохраняется файл в выделенной директории.
        Возвращается response, содержащий URL страницы, открываемой после добавления.
        """
        author_username = 'noname_author'
        if current_user and current_user.is_authenticated:
            author_username = current_user.username
        else:
            flash("Ошибка: Пользователь не авторизован для добавления датасета.", "danger")
            response: Response = make_response()
            response.headers['redirect'] = url_for('auth.login')
            return response


        form_values: DatasetFormValues = DatasetController._extract_form_values(request)
        
        if form_values.dataset_data is None and request.files.get('dataset') and request.files['dataset'].filename != '':
             flash("Ошибка при обработке файла датасета. Пожалуйста, убедитесь, что файл в кодировке UTF-8.", "danger")
             response: Response = make_response()
             response.headers['redirect'] = url_for('datasets.render_add_dataset') 
             return response


        upload_folder_path_str: str = current_app.config['UPLOAD_FOLDER']
        dataset_id = DatasetService.save_dataset(form_values, author_username=author_username, filepath=upload_folder_path_str)

        if form_values.dataset_data is not None:
            filepath_to_save = Path(upload_folder_path_str) / f'{dataset_id}.csv'
            filepath_to_save.parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(filepath_to_save, 'w', encoding='utf-8') as file:
                    file.write(form_values.dataset_data)
            except Exception as e:
                current_app.logger.error(f"Error writing dataset file {filepath_to_save}: {e}")
                flash("Датасет добавлен в базу, но произошла ошибка при сохранении файла.", "warning")
        else:
            flash("Файл датасета не был загружен или не удалось его обработать.", "warning")


        response: Response = make_response()
        response.headers['redirect'] = '/datasets/'
        return response

    @staticmethod
    def render_add_dataset() -> str:
        """
        Отображает страницу добавления датасета.
        """
        return render_template('add_dataset.html')

    @staticmethod
    def render_edit_dataset(dataset_id: str) -> str:
        """
        Обращается к методу сервиса для получения объекта Brief для датасета с индексом dataset_id.
        """
        dataset_brief: Dataset = DatasetService.get_dataset(dataset_id)
        return render_template('edit_dataset.html', dataset_brief=dataset_brief)

    @staticmethod
    def remove_dataset(dataset_id: str) -> Response:
        """
        Обращается к методу сервиса для удаления объекта датасета с индексом dataset_id.
        """
        DatasetService.remove_dataset(dataset_id)

        filepath: str = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(filepath, f'{dataset_id}.csv')
        PosixPath(filepath).unlink()

        response: Response = make_response()
        response.headers['redirect'] = f'/datasets/{dataset_id}'
        return response

    @staticmethod
    def get_dataset(dataset_id: str) -> Dataset:
        """
        Возвращается структура, содержащая данные о датасете.
        """
        dataset: Dataset = DatasetService.get_dataset(dataset_id)
        return dataset

    @staticmethod
    def _extract_form_values(request: Request) -> DatasetFormValues:
        form_data = request.form
        dataset_name: str = form_data.get('name', '').strip()
        dataset_description: str = form_data.get('description', '').strip()

        dataset_data_str: str | None = None
        dataset_fs: FileStorage | None = request.files.get('dataset')

        if dataset_fs and dataset_fs.filename:
            current_app.logger.debug(f"Processing uploaded file: {dataset_fs.filename}")
            try:
                file_content_bytes = dataset_fs.read()
                dataset_data_str = file_content_bytes.decode('utf-8').strip()
                if not dataset_data_str:
                    dataset_data_str = None
                    current_app.logger.debug("Uploaded file content is empty after stripping.")
            except UnicodeDecodeError:
                current_app.logger.warning(
                    f"UnicodeDecodeError processing file {dataset_fs.filename}. Trying latin-1."
                )
                try:
                    dataset_fs.seek(0) 
                    file_content_bytes = dataset_fs.read()
                    dataset_data_str = file_content_bytes.decode('latin-1').strip()
                    if not dataset_data_str: dataset_data_str = None
                except Exception as e_latin1:
                    current_app.logger.error(
                        f"Could not decode file {dataset_fs.filename} with UTF-8 or latin-1: {e_latin1}"
                    )
                    dataset_data_str = None
            except Exception as e:
                current_app.logger.error(f"Error reading file content from {dataset_fs.filename}: {e}")
                dataset_data_str = None
        else:
            current_app.logger.debug("No new file uploaded or file field was empty.")
            
        return DatasetFormValues(dataset_name, dataset_description, dataset_data_str)

    @staticmethod
    def edit_dataset(dataset_id: str, request: Request) -> Response:
        editor_username = 'noname_editor'
        if current_user and current_user.is_authenticated:
            editor_username = current_user.username
        else:
            return jsonify({"success": False, "message": "Ошибка: Пользователь не авторизован."}), 401

        form_values: DatasetFormValues = DatasetController._extract_form_values(request)
        upload_folder_directory: str = current_app.config['UPLOAD_FOLDER']

        if request.files.get('dataset') and request.files.get('dataset').filename and form_values.dataset_data is None:
            return jsonify({"success": False, "message": "Ошибка при обработке загруженного файла. Файл не был обновлен. Пожалуйста, проверьте кодировку (UTF-8)."}), 400

        if form_values.dataset_data is not None and request.files.get('dataset') and request.files.get('dataset').filename:
            full_csv_path_to_write = Path(upload_folder_directory) / f'{dataset_id}.csv'
            full_csv_path_to_write.parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(full_csv_path_to_write, 'w', encoding='utf-8') as file_out:
                    file_out.write(form_values.dataset_data)
            except Exception as e:
                current_app.logger.error(f"Error writing updated dataset file {full_csv_path_to_write}: {e}")
                
        try:
            DatasetService.update_dataset(dataset_id, form_values, 
                                          editor_username=editor_username, 
                                          filepath=upload_folder_directory)
            
            success_message = "Информация о датасете успешно обновлена."
            redirect_url_target = url_for('datasets.get_dataset', dataset_id=dataset_id, _external=False)
            return jsonify({
                "success": True, 
                "message": success_message, 
                "redirect_url": redirect_url_target
            }), 200

        except Exception as e:
            current_app.logger.error(f"Error in DatasetService.update_dataset for {dataset_id}: {e}", exc_info=True)
            return jsonify({"success": False, "message": "Произошла ошибка при обновлении информации о датасете."}), 500