class NoFilesUploaded(Exception):
    def __init__(self, file, *args):
        super().__init__(args)
        self.file = file
    def __str__(self):
        return f"No files were found uploaded in the \"{self.file}\" files"
        
