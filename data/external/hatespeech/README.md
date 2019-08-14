# Hate Spech Data

## Original Data
This data comes from two of Zeerak Waseems's studies (see below for references). The data was originally split across four .json files comprised of Tweets and (some of) their associated meta-data, in addition to an annotation. These annotations are one of `"racism"`, `"Sexism"`, `"sexism"`, `"Both"`, `"none"`, or `"Neither"`.

## Wrangled Data
To format the data for use in Opt Out:  

- The data was imported and converted to data frames.  
- With the exception of the annotation column, any column which didn't appear in the AWS data sets were dropped to keep consistency across data sets (*NB*: not all columns from the AWS data were available).  
- The `"racism"` Tweets were dropped.  
- All "Both" annotation labels were relabeled to "sexism" (as the Tweets contains elements of sexism).  
- The annotation labels were renamed to `not_misogynistic` and `misogynistic` to keep consistency with the prodigy framework being used to annotate the AWS Tweets.  
- Duplicate Tweets were removed.  
- As there were more non_misogynistic than misogynistic Tweets, the classes were balanced using random sampling.  
- The final data set contains 8484 annotated Tweets.  

## References

This dataset aggregates datasets related to these academic works[[1]](http://aclweb.org/anthology/W16-5618)[[2]](http://www.aclweb.org/anthology/N16-2013). We and Zeerak request that you cite both if you use this dataset.

```
@InProceedings{waseem:2016:NLPandCSS,
  author    = {Waseem, Zeerak},
  title     = {Are You a Racist or Am I Seeing Things? Annotator Influence on Hate Speech Detection on Twitter},
  booktitle = {Proceedings of the First Workshop on NLP and Computational Social Science},
  month     = {November},
  year      = {2016},
  address   = {Austin, Texas},
  publisher = {Association for Computational Linguistics},
  pages     = {138--142},
  url       = {http://aclweb.org/anthology/W16-5618}
}

@InProceedings{waseem-hovy:2016:N16-2,
  author    = {Waseem, Zeerak  and  Hovy, Dirk},
  title     = {Hateful Symbols or Hateful People? Predictive Features for Hate Speech Detection on Twitter},
  booktitle = {Proceedings of the NAACL Student Research Workshop},
  month     = {June},
  year      = {2016},
  address   = {San Diego, California},
  publisher = {Association for Computational Linguistics},
  pages     = {88--93},
  url       = {http://www.aclweb.org/anthology/N16-2013}
}
```

