from multiprocessing import Pool

from database.db import DB
from offertFactory import OffertFactory

# from factories import itPracujPl
from factories import justJoin
from factories import noFluffJobs
from factories import bullDogJob


class OffertCron:
    # def __init__(self) -> None:
    #     self.modules = list(
    #         filter(
    #             lambda x: x.endswith(".py") and x != "__init__.py",
    #             os.listdir("factories"),
    #         )
    #     )
    #     self.import_modules()

    # def get_all_subclasses(self, factory):
    #     """List all subclasses which inherit from factory"""

    #     all_subclasses = []
    #     for subclass in factory.__subclasses__():
    #         all_subclasses.append(subclass)
    #         all_subclasses.extend(self.get_all_subclasses(subclass))

    #     print(factory.__subclasses__())

    #     return all_subclasses

    # def import_modules(self):
    #     """Import all modules from factories folder"""
    #     PATH = os.getcwd()
    #     for module in self.modules:
    #         spec = importlib.util.spec_from_file_location(
    #             module, PATH + "/factories/" + module
    #         )
    #         foo = importlib.util.module_from_spec(spec)
    #         sys.modules[module] = foo
    #         spec.loader.exec_module(foo)

    def setup_cron(self):
        """Setup cron every 2.0s"""

        # TODO: Setup cron for given time

        self.scrap()

    def scrap_from_factory(self, factory: OffertFactory):
        """Scrap all offerts from given factory"""

        offerts = factory.get_offerts()
        DB.insert_offerts(offerts)

    def scrap(self):
        """Scrap all offerts from all factories"""

        factories = [
            noFluffJobs.NoFluffJobs,
            justJoin.JustJoinOfferts,
            bullDogJob.BullDogJob,
        ]

        pool = Pool(processes=len(factories))

        results = pool.map(self.scrap_from_factory, factories)

        for result in results:
            print(result)


if __name__ == "__main__":
    offert_cron = OffertCron()
    offert_cron.setup_cron()
