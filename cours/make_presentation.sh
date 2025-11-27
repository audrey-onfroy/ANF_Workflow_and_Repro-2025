# run this within the current workdir
pandoc -t revealjs \
       -s slides.md \
       -o slides.html \
       -V revealjs-url=reveal.js-master \
       -V theme=white \
       --include-in-header=slides.css \
       --metadata-file slides.metadata \
       --embed-resources 
