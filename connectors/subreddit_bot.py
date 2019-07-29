def is_valid_multi_name(name: str):
    if 2 > len(name) > 50:
        return False
    alphanumerics = 2
    for ch in name:
        if '0' <= ch <= '9' or 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            alphanumerics -= 1
            if alphanumerics == 0:
                return True
    return False


# the generic subreddit bot used to connect to different mediums of user interaction (such as the GUI or terminal)
class SubredditBot:

    # method used to send the error to the current medium
    def send_error(self, error):
        raise NotImplementedError()

    # generic method used to write to the medium
    def write_to_screen(self, to_write):
        raise NotImplementedError()

    # method used to write to the medium during create
    def create_write(self, to_write):
        raise NotImplementedError()

    # method used to read the relevant data for create
    def create_read(self, reddit):
        raise NotImplementedError()

    # method used to write to the medium during backup
    def backup_write(self, to_write):
        raise NotImplementedError()

    # method used to read the relevant data for backup
    def backup_read(self, reddit):
        raise NotImplementedError()

    # method used to write to the medium for mimic
    def mimic_write(self, to_write):
        raise NotImplementedError()

    # method used to read the relevant data for mimic
    def mimic_read(self, reddit):
        raise NotImplementedError()

    # method used to write to the medium for save
    def save_write(self, to_write):
        raise NotImplementedError()

    # method used to read the relevant data for save
    def save_read(self, reddit):
        raise NotImplementedError()

    # method used to write to the medium for unsave
    def unsave_write(self, to_write):
        raise NotImplementedError()

    # method used to read the relevant data for unsave
    def unsave_read(self, reddit):
        raise NotImplementedError()

