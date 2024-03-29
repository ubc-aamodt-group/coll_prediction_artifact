python scene_generator.py
for i in {0..99}
do
    for j in dens3 dens6 dens9 dens12
    do  
        python pred_trace_generation.py 1000 scene_benchmarks/${j} ${i}
    done
done
