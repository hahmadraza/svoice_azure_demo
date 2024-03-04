tr=egs/dataset/tr
ts=egs/dataset/ts
vl=egs/dataset/vl
mkdir -p $tr
mkdir -p $ts
mkdir -p $vl

CPATH=`pwd`
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/dev/mix_both" > "egs/dataset/vl/mix.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/dev/s1" > "egs/dataset/vl/s1.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/dev/s2" > "egs/dataset/vl/s2.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/dev/s3" > "egs/dataset/vl/s3.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/dev/s4" > "egs/dataset/vl/s4.json"


python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/test/mix_both" > "egs/dataset/ts/mix.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/test/s1" > "egs/dataset/ts/s1.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/test/s2" > "egs/dataset/ts/s2.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/test/s3" > "egs/dataset/ts/s3.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/test/s4" > "egs/dataset/ts/s4.json"

python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/train-360/mix_both" > "egs/dataset/tr/mix.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/train-360/s1" > "egs/dataset/tr/s1.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/train-360/s2" > "egs/dataset/tr/s2.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/train-360/s3" > "egs/dataset/tr/s3.json"
python -m svoice.data.audio $CPATH"/mnt2/Libri4Mix_Dataset_v1/Libri4Mix/wav16k/min/train-360/s4" > "egs/dataset/tr/s4.json"

