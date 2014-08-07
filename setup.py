# Run the zetup script (reading config from zetuprc):
exec(open('__init__.py').read())


zetup(
  package_dir={
    'modeled.zetup': '.',
    },
  packages=[
    'modeled',
    'modeled.zetup',
    'modeled.member',
    'modeled.cfunc',
    ],
  package_data={
    'modeled.zetup': ZETUP_DATA,
    },
  )
