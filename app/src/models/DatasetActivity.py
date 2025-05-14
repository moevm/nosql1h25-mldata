class DatasetActivity:
    def __init__(self,dataset_id , activity_dict: dict):
        self.dataset_id = dataset_id
        activities = sorted(activity_dict['statistics'].items())
        self.statistics = {
            'dates': [],
            'views': [],
            'downloads': []
        }
        with open('/tmp/log.txt', 'w') as f:
            f.write(str(activities))

        for i in activities:
            self.statistics['dates'].append(i[0])
            self.statistics['views'].append(i[1]['views'])
            self.statistics['downloads'].append(i[1]['downloads'])
    
        
