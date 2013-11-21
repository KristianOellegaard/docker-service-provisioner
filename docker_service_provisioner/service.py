import string
import random


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class DockerService(object):
    dockerfile = ""
    configuration = {

    }


class RandomGenerator(object):
    def generate(self):
        raise NotImplementedError()


class RandomText(RandomGenerator):
    def generate(self):
        return random_generator(16)