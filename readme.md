


#Task 3
## WITHOUT DOCKER
* py -3 lensa_api.py --storage=file --backup_file=db.json


## WITH DOCKER
##1.) Setup
* docker pull tamasmagyar/lensa_hw:1.1 
#####OR
* change directory to "task 3" 
* docker build -t lensa_api .      

     
##2.) Run
docker run  -p 5000:5000 tamasmagyar/lensa_api:1.1  --storage=mem --backup_file=asd.json


##3.) Example usage
* curl -v -GET -H "Content-type: application/json" "127.0.0.1:5000/"
#####OR
* from POSTMAN

## 4.) Copying result from container to local.
docker ps
   * Get container id      
* docker cp <docker_container_id>:app/<RESULTS.json> results.json