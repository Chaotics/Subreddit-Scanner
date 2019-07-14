class SubredditBot:
    def send_error(self, error):
        raise NotImplementedError()

    def write_to_screen(self, to_write):
        raise NotImplementedError()

    def create_write(self, to_write):
        raise NotImplementedError()

    def create_read(self, reddit):
        raise NotImplementedError()

    def backup_write(self, to_write):
        raise NotImplementedError()

    def backup_read(self, reddit):
        raise NotImplementedError()

    def mimic_write(self, to_write):
        raise NotImplementedError()

    def mimic_read(self, reddit):
        raise NotImplementedError()

    def save_write(self, to_write):
        raise NotImplementedError()

    def save_read(self, reddit):
        raise NotImplementedError()

    def reset_write(self):
        raise NotImplementedError()
