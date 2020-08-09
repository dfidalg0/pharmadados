from apscheduler.schedulers.background import BackgroundScheduler
from medicines.models import Medicine, Source, Info
from concurrent.futures import ThreadPoolExecutor
from pickle import loads


def param(q):
    def apply(f):
        return f(q)

    return apply


def update():
    print('Performing database update...')

    sources = Source.objects.all()
    for medicine in Medicine.objects.iterator():
        query = param(medicine.name)
        functions = list(
            map(loads, map(lambda s: s.scrap_function, sources))
        )

        with ThreadPoolExecutor(max_workers=2*len(functions)) as pool:
            results = list(pool.map(query, functions))

        to_create = []

        for i, source in enumerate(sources):
            for result in results[i]:
                to_create.append(
                    Info(medicine=medicine, source=source, **result)
                )

        Info.objects.bulk_create(to_create, ignore_conflicts=True)

    print(f'Database update completed')


def run():
    scheduler = BackgroundScheduler()

    ThreadPoolExecutor().submit(update)

    scheduler.add_job(update, 'interval', hours=3)

    scheduler.start()
