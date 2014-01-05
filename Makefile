# These targets are not files
.PHONY: install upgrade coverage i18n lint

fs:
	foreman start -f Procfile.local

rs:
	python manage.py runserver

install:
	pip install -r reqs/dev.txt --use-mirrors

upgrade:
	pip install --upgrade -r reqs/dev.txt --use-mirrors

coverage:
	coverage run ./runtests.py --with-xunit
	coverage html -i

lint:
	./lint.sh

messages:
	# Create the .po files used for i18n
	cd oscar; django-admin.py makemessages -a

compiledmessages:
	# Compile the gettext files
	cd oscar; django-admin.py compilemessages

css:
	lessc {{ project_name }}/assets/css/styles.scss {{ project_name }}/assets/css/styles.css
	autoprefixer {{ project_name }}/assets/css/styles.css

cssw:
	kicker -e "make css" {{ project_name }}/assets/css/

clean:
	# Remove files not in source control
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov *.egg-info *.pdf dist violations.txt
