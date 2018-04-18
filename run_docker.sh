docker build -t nitro .
docker run -ti --name=nitro nitro
docker cp nitro:/usr/src/nitro/results/allrows.tsv ./results/allrows.tsv
