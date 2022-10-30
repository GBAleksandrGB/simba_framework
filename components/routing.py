class Router:
    def __init__(self, request, routes: dict):
        self.request = request
        self.routes = self.routes_process(routes)

    @staticmethod
    def routes_process(routes):
        res = []
        for path, view in routes.items():
            path_dict = {
                'path': [],
                'view': view
            }
            path = path.strip('/')
            path_list = path.split('/')
            is_var = False
            for part in path_list:
                value = part
                if '<' in part:
                    value = part.strip('<').strip('>')
                    is_var = True
                path_dict['path'].append({'value': value, 'is_var': is_var})
            res.append(path_dict)
        return res

    def get_view(self, path, view_404):
        path_list = path.strip('/').split('/')
        url_vars = {}
        for route in self.routes:
            if len(path_list) == len(route['path']):
                check_list = [False]*len(path_list)
                for i, part in enumerate(route['path']):
                    if part['is_var']:
                        url_vars[part['value']] = path_list[i]
                        check_list[i] = True
                    else:
                        if part['value'] == path_list[i]:
                            check_list[i] = True
            else:
                continue

            if not (False in check_list):

                self.request['url_vars'] = url_vars
                return route['view']
            else:
                continue
        return view_404
