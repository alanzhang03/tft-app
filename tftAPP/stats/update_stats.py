from models import Augment

def main():
    settings.configure()
    augments = []
    a = Augment(name="Gifts from the Fallen", two_one=3.22, three_two = 2.13, four_one=3.12)
    a.save()


if __name__ == '__main__':
    main()
