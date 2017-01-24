#include <sys/types.h>
#include <sys/stat.h>
#include <sys/times.h>
#include "obj.h"
#include "index.h"

extern long long numDistances;
int main (int argc, char **argv)

   { char str[1024];
     Index S;
     int k;
     Tdist r;
     struct stat sdata;
     struct tms t1,t2, start;
     unsigned int numQueries = 0;

     if (argc != 2)
        { fprintf (stderr,"Usage: %s index-file\n",argv[0]);
          exit(1);
        }

     fprintf (stderr,"reading index...\n");
     S = loadIndex (argv[1]);
     stat (argv[1],&sdata);
     fprintf (stderr,"read %lli bytes\n",(long long)sdata.st_size);

     numDistances = 0;
	 times(&start);
     while (true)
        {
			long long sdist = numDistances;
			Obj qry;
	  int siz;
	  bool fixed;

          if (scanf ("%[0123456789-.]s",str) == 0) break;
	  if (!strcmp(str,"-0")) break; // -0 -> terminate

          if (str[0] == '-') // negative => kNN
             { fixed = false;
               if (sscanf (str+1,"%d",&k) == 0) break; // syntax error
	     }
          else  // range query
             { fixed = true;
#ifdef CONT
               if (sscanf (str,"%f",&r) == 0) break; // syntax error
#else
               if (sscanf (str,"%d",&r) == 0) break; // syntax error
#endif
	     }
	  if (getchar() != ',') break; // syntax error
	  if (scanf ("%[^\n]s",str) == 0) break; // syntax error
	  if (getchar() != '\n') break; // syntax error
	  qry = parseobj (str);

          numQueries++;
          if (fixed)
	     { times(&t1);
	       siz = search(S,qry,r,true);
	       times(&t2);
               fprintf (stderr,"objects found=%i\n",siz);
	     }
	  else
	     { times(&t1);
	       r = searchNN (S,qry,k,true);
	       siz = k;
	       times(&t2);
		   long long tdist = numDistances - sdist;
#ifdef CONT
               fprintf (stderr,"kNNs at distance=%f\ttime=%f\tcalcs=%ld\ttndistances=%ld\n",r, difftime(t2,t1), tdist,numDistances);
#else
               fprintf (stderr,"kNNs at distance=%i\ttime=%f\tcalcs=%ld\n",r, difftime(t2,t1),tdist);
#endif
	     }
	}
    times(&t2);
    fprintf(stderr,"tdistancecalcs=%ld\tnumqueries=%ld \n", numDistances, numQueries);
     fprintf(stderr,"Total distances per query=%f\ttotaltime=%f (s)\tavgtime=%.f (s)\n",
		(float)numDistances/(float)numQueries, difftime(t2,start), (float) (difftime(t2,start)/(float)numQueries));
     fprintf (stderr,"freeing...\n");
     freeIndex (S,true);
     fprintf (stderr,"done\n");
	   return 0;
   }

