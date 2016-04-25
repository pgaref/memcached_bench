# memcached_bench

## How to use memaslap to benchmark memcached. I used:
* Memcached 1.4.14 (installed from Ubuntu packages)
* memaslap from libmemcached using QJump [patch](http://www.cl.cam.ac.uk/research/srg/netos/qjump/login2015/figure1b.html)

## In order to build libmemcached including memaslap. Inside the git repo path run:
* cd libmemcached-1.0.15/
* ./configure --enable-memaslap
* make && sudo make install

## To run memcached, use the configuration below:
* /usr/bin/memcached -m 64 -p 11211 -u memcache 

## To run memaslap benchmark:
* ../clients/memaslap -s 127.0.0.1:11211 -S 1s -B -T2 -c 128 > out


## For graphs, install matplotlib
* Ubuntu: sudo apt-get install python-matplotlib
* MacOs: pip install matplotlib
