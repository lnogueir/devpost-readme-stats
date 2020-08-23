from modules.hacker_fetcher import HackerFetcher
import random

class HackerRequestHandler:
    REQ_PARAMS_LIST = [
        'skills_count',
        'projects_count',
    ]

    def __init__(self):
        self.optional_parameters = None
        self.request_result = None
    
    def set_optional_parameters(self, hacker_request):
        try:
            skills_count = int(hacker_request.get(self.REQ_PARAMS_LIST[0]))
        except:
            skills_count = None
        
        try:
            projects_count = int(hacker_request.get(self.REQ_PARAMS_LIST[1]))
        except:
            projects_count = None
        
        self.optional_parameters = {
            self.REQ_PARAMS_LIST[0]: skills_count,
            self.REQ_PARAMS_LIST[1]: projects_count,
        }

    def process(self, hacker_request):
        if 'id' in hacker_request:
            hacker_id = hacker_request.get('id')
            # TODO: raise ValueError in case hacker_id is not found on devpost
            fetcher = HackerFetcher(hacker_id)
            projects = fetcher.get_projects()
            skills = fetcher.get_skills()
            random.shuffle(projects)
            projects.sort(reverse=True, key=lambda p: p['is_winner'])
            random.shuffle(skills)
            self.set_optional_parameters(hacker_request)
            return {
                'hacker_name': fetcher.get_hacker_name(),
                'hacker_id': hacker_id,
                'hacker_url': fetcher.url,
                'hackathon_count': fetcher.get_hackathon_count(),
                'projects': projects[:projects_count] if (projects_count := self.optional_parameters[self.REQ_PARAMS_LIST[1]]) != None else projects,
                'win_count': len(list(filter(lambda project: project['is_winner'], projects))),
                'skills': skills[:skills_count] if (skills_count := self.optional_parameters[self.REQ_PARAMS_LIST[0]]) != None else skills,
            }
        raise KeyError('id must be present in request')
