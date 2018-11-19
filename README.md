# Potential-Aware-Abstraction-In-Texas-Hold-em-Poker
This code is based on the implementation of http://www.cs.cmu.edu/afs/cs/Web/People/sandholm/potential-aware_imperfect-recall.aaai14.pdf
you can read it to understand its details.

The project is based on the two algorithms below.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181119124849580.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTY3OTQxMQ==,size_16,color_FFFFFF,t_70)

It is not friendly in computing the EMD distance between two distribution. so in this paper, it proposed the approxiamating EMD distance for  high dimensional and sparse case. It should be noted that it is not necessary to compute EMD distance in all condition.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181119124856106.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTY3OTQxMQ==,size_16,color_FFFFFF,t_70)
### Usage:
When you want to use abstraction in Texas Hold’em, you should use :
```
	python generate_data_5public.py
```
to generate the data you need in the 5th hand card
You can modified the placeholder to store the generated data.
After that, you could use:
```
	python clustering_5public.py 
```
to cluster the data generate by the program generate_data_5_public. You may modify catalog to the placeholder you define before.
Program cluster_5public.py will generate the centroids of clusters to use in the generate_data_4public.py.
Do the same thing for twice, you will get the final results. You should pay attention to that the project is for 12 cards. You may change the cards number when you use in 52 cards.



### NOTE：
judging.py is a script which could help you judge which side will win in the last round. You can use it more than there.

If you read the paper upper carefully, you will understand that heuristic algorithm for calculating EMD distance is only need in the high dimensional and sparse case. So I write my code in that way. 

As illustrated in the paper, it needs massive computing power to get results in 52 cards.

