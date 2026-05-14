In this subfolder of the repo, you will place your training data. You typically want a 80/10/10 or 70/20/10 split; Train/Valid/Test setup.

This dataset should look something like this:

/dataset
├── data.yaml
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/ (Optional)
    ├── images/
    └── labels/

    The only path that is strictly necessary is train. You can typically just use train data for valid, just point the path there, and you can also disregard test. As such, you can use an 80/20 Train/Valid Split if you want to skip test. otherwise, just point valid to train as well. 



    If all of your images are train, you can simply put your data in this same folder, like this:

    /dataset
├── data.yaml
├── train/
│   ├── images/
│   └── labels/

Just ensure that you have a yaml and train/images as well as train/labels. If you do, you are ready to run the program, and on run, it will ask you if you want to create a 80/20 split.