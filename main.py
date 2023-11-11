import io
import pprint

from data.constant import CONSTANTS


pp = pprint.PrettyPrinter()


class Reader:
    def __init__(self, file: io):
        """
        Initialize class and set some private class values.

        :param file: java compiled .class file opened with 'rb', 'read_bytes'.
        """
        self.file = file
        self.__meta = {}
        self.__constant_pool = []
        self.__constant_pool_count = 0
        self.__constants = CONSTANTS

    def __read_bytes(self, amount: int):
        """
        Reads the byte values in the file, io bytes object.

        :param amount: Amount of bytes to read.
        :return: value of the bytes.
        """
        return int.from_bytes(self.file.read(amount), 'big')

    def __read_meta(self):
        """
        Reads the magic first few and other meta bytes.

        :return: Nothing.
        """

        self.__meta['magic'] = hex(self.__read_bytes(4))
        self.__meta['minor'] = self.__read_bytes(2)
        self.__meta['mayor'] = self.__read_bytes(2)
        self.__constant_pool_count = self.__read_bytes(2)

    def parse(self):
        """
        Parse the byte file, and check if key is in the constants dict and using the values and keys from this dict.
        The correct bytes and corresponding values are appended to a pool, which in turn gets added to the meta dict.

        :return: dict with all read values.
        """
        self.__read_meta()
        pool = []
        for i in range(self.__constant_pool_count - 1):
            key, values = self.__read_bytes(1), {}
            value_dict = self.__constants.get(key)
            if not value_dict:
                raise NotImplementedError(f'Unexpected key of {key} found, data/constant.py has implemented methods')
            for key, value in value_dict.items():
                if key != 'tag':
                    values[key] = self.__read_bytes(value)
                    if key == 'length':
                        values['bytes'] = self.file.read(values[key])
                        break
                    continue
                values['tag'] = value
            pool.append(values)
        self.__meta['pool'] = pool
        return self.__meta


def main():
    with open('data/Main.class', 'rb') as file:
        meta = Reader(file).parse()
        pp.pprint(meta)


if __name__ == '__main__':
    main()
