# FastLane

### Running Guide

#### DB

1. sudo docker run --name "fl_postgis" -p 25432:5432 -d -t kartoza/postgis -e POSTGRES_USER=fastlane -e POSTGRES_PASS=1234 -e POSTGRES_DBNAME=fastlanes --network=fastlanes_nt
