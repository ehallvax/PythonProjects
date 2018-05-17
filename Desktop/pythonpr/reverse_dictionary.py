import datetime
now = datetime.datetime.now()


class Person:
    salary = 10
    def __init__(self,first_name,last_name,birth_year):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
    @property
    def full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)
    def get_age(self):
        return now.year - self.birth_year
    @classmethod
    def from_full_name(cls,full_name,birth_year):
        first_name,last_name = full_name.split(' ')
        return cls(first_name,last_name,birth_year)
    def __repr__(self):
        return "\"Person(first_name={}, last_name={}, birth_year={})\"".format(self.first_name,self.last_name,self.birth_year)


def main():
    p = Person(first_name='John', last_name='Doe', birth_year=1960)

    print(p.first_name)
    print(p.last_name)
    print(p.full_name)
    print(p.get_age())  # This should be a method call. (Return years).

    # Use a `@classmethod` to create this alternative constructor.
    p = Person.from_full_name('John Doe', birth_year=1980)
    print(p.last_name)  # Should print 'Doe'
    print(p)  # Should print "Person(first_name='John', last_name='Doe', birth_year=1980)"

if __name__ == '__main__':
    main()