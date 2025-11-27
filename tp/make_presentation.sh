# run this within the current workdir
pandoc -t html \
       -s \
       --include-in-header=tp.css \
       -V theme=white \
       --metadata-file tp.metadata \
       --embed-resources \
       -f markdown \
       tp.md -o tp.html --toc
