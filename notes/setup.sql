#!/bin/bash
psql -h tv1 -U neeladasgupta -p 5432 -d rental_accounting -f db/schema.sql
psql -h tv1 -U neeladasgupta -p 5432 -d rental_accounting -f db/seed.sql
#psql postgressql://neeladasgupta@tv1:5432/rental_accounting -f db/schema.sql
