mkdir logfiles_BIT_link
python eval_all.py 2000 BIT*
for i in {2000..2199}
do  
    python read_logfile.py ${i}
done
