pg_isready -q || service postgresql start >/dev/null 2>&1
mysqladmin -uroot ping >/dev/null 2>&1 || service mysql start >/dev/null 2>&1
for i in 1 2 3 4 5; do pg_isready -q && break; sleep 1; done
for i in $(seq 1 30); do mysqladmin -uroot ping >/dev/null 2>&1 && break; service mysql start >/dev/null 2>&1; sleep 1; done
