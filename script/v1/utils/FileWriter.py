class FileWriter:
    def __init__(self, destination):
        self.destination = destination
    # end __init__()

    def create(self, filename, contents):
        """
        Write text content to a new file in the FileWriter's destination folder.

        Parameters:
            filename (str): what the file should be called. e.g. 'example.txt'
            contents (str): what text should be written to the file

        Returns:
            (None)
        """
        new_file_path = f"{self.destination}/{filename}"
        with open(new_file_path, 'w') as file:
            file.write(contents)
    # end create_new_file()
