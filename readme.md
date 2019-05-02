# Task 1

Reads inputs from input.txt

# Task 3

## WITHOUT DOCKER

*     py -3 lensa_api.py --storage=file --backup_file=db.json
    - Note: requirements are in requirements.txt

## WITH DOCKER


## 1.) Run docker 
    run -p 5000:5000 tamasmagyar/lensa_api:latest --storage=file --backup_file=storage.json

## 2.) Example usage 
*     curl -v -GET -H "Content-type: application/json" "127.0.0.1:5000/" 
##### OR

-   from POSTMAN

## Copying result from container to local.

*     docker ps

	-   Get container id
    
-   Then:
    
    ```
       docker cp <docker_container_id>:app/<RESULTS.json> results.json    
    ```
    
    -   Note: default result file is 'backup.json"
    
    
# Tests

Can only run on local machine.
