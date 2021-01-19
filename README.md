# Introduce about TopDup 
TopDup is a project that start from a forum [Forum Machine Learning Cơ bản](https://www.facebook.com/groups/machinelearningcoban) nhằm which aiming to help the website, blogger from prevent copyright problem.

The idea is to crawling all of the blog from more than 1000 website everyday and using NLP techniques to calculate the similarity score between the original one with the rest to figure out which one is copying the original blog . 

This project is an effort in preventing stealing other people work that happen recently in Vietnam. For more information please read [Topdev copy Viblo work without permission](https://www.facebook.com/groups/machinelearningcoban/permalink/1036374896819917)   

# Project structure
TopDup split into 5 main group so that everyone can work and contribute in. This included:
1. Crawl Data
2. Data wrangling
3. NLP Model
4. API Connection
5. Web

![High Level Architecture](docs/topdup_highlevel.png)

# Folder Structure 
~~~
/modules: contains all the source code of project. Split base on team
    /crawlers: Scan and craw information 
    /data_wranglers: Preprocessing and Cleaning 
    /ml: Source code for AI/ML 
    /ml_api: API Connection
    /web_app: Front + Back end
    /legacies: TopDup old version
        /topdup_open: Source code on scanning and front end 
        /docbao: Scan using DocBao API
~~~
