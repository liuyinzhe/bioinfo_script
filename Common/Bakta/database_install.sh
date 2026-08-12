#https://raw.githubusercontent.com/oschwengers/bakta/main/db-versions.json
    {
        "date": "2025-02-24",
        "major": 6,
        "minor": 0,
        "doi": "10.5281/zenodo.14916843",
        "record": "14916843",
        "md5": "4c1115e40abfa2b464ae5dd988bdd88e",
        "md5-light": "4a6e059ded39e9c5537ef4137d2f5648",
        "software-min": {
            "major": 1,
            "minor": 11
        }
    }

wget https://zenodo.org/record/14916843/files/db-light.tar.xz
wget https://zenodo.org/record/14916843/files/db.tar.xz

db_url = f"https://zenodo.org/record/{required_version['record']}/files/{'db-light' if args.type == 'light' else 'db'}.tar.xz"

bakta_db install -i db.tar.xz
