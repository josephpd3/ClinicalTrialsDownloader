# Clinical Trials Research Downloader

### Summary

This program downloads research of specified criteria from clinicaltrials.gov and stores said research in Pandas DataFrames on disk.

### Specifying Search Parameters

This program can download research for any number of criteria as specified in a text file in the root directory of the program titled *params.txt*.

Each line of this file specifies separate search criteria which will be used
to gather results for that criteria in a folder within *root_directory*/downloads/*criteria*.

For example, say you want to look up trials and research relevant to lung transplants, seizures, and brain tumors. You will format the file as such:

*params.txt*
```
lung transplant
seizure
brain tumor
```

Once this file is in place, just run the program as normal and it will retrieve all the relevant research!