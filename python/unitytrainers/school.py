"""Contains the School class."""

import os
from unitytrainers import Curriculum

class School(object):
    """A School holds curriculums. Each curriculum is associated to a particular
    brain in the environment.
    """

    def __init__(self, curriculum_folder, default_reset_parameters):
        """Initializes a School object.

        Args:
            curriculum_folder (str): The relative or absolute path of the
                folder which holds the curriculums for this environment.
                The folder should contain JSON files whose names are the
                brains that the curriculums belong to.
            default_reset_parameters (dict): The default reset parameters
                of the environment.
        """
        if curriculum_folder is None:
            self._brains_to_curriculums = None
        else:
            self._brains_to_curriculums = {}
            for curriculum_filename in os.listdir(curriculum_folder):
                brain_name = curriculum_filename.split('.')[0]
                curriculum_filepath = \
                    os.path.join(curriculum_folder, curriculum_filename)
                self._brains_to_curriculums[brain_name] = \
                    Curriculum(curriculum_filepath, default_reset_parameters)

    @property
    def brains_to_curriculums(self):
        """A dict from brain_name to the brain's curriculum."""
        return self._brains_to_curriculums

    @property
    def lesson_nums(self):
        """A dict from brain name to the brain's curriculum's lesson number."""
        lesson_nums = {}
        for brain_name, curriculum in self.brains_to_curriculums:
            lesson_nums[brain_name] = curriculum.lesson_num

        return lesson_nums

    @lesson_nums.setter
    def lesson_nums(self, lesson_nums):
        for brain_name, lesson in lesson_nums.items():
            self.brains_to_curriculums[brain_name].lesson_num = lesson

    def increment_lessons(self, progresses):
        """Increments all the lessons of all the curriculums in this School.

        Args:
            progresses (dict): A dict of brain name to progress.
        """
        for brain_name, progress in progresses.items():
            self.brains_to_curriculums[brain_name].increment_lesson(progress)


    def set_all_curriculums_to_lesson_num(self, lesson_num):
        """Sets all the curriculums in this school to a specified lesson number.

        Args:
            lesson_num (int): The lesson number which all the curriculums will
                be set to.
        """
        for _, curriculum in self.brains_to_curriculums.items():
            curriculum.lesson_num = lesson_num


    def get_config(self):
        """Get the combined configuration of all curriculums in this School.

        Returns:
            A dict from parameter to value.
        """
        config = {}

        for _, curriculum in self.brains_to_curriculums.items():
            curr_config = curriculum.get_config()
            config.update(curr_config)

        return config
