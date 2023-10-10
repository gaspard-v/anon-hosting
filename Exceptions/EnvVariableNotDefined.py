class NoFilesUploaded(Exception):
    def __init__(self, file, *args):
        super().__init__(args)
        self.file = file

    def __str__(self):
        return f'No files were found uploaded in the "{self.file}" files'


class EnvVariableNotDefined(Exception):
    def __init__(self, env_variable_name, *args):
        super().__init__(args)
        self.env_variable_name = env_variable_name

    def __str__(self):
        return f'Environment variable "{self.env_variable_name}" is not defined !'
