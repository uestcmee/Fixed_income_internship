# 中证500的回测

## 做了什么

其实要说的话主体功能还是和上一次的差不多大概做了的事

* 重新规划了一下结构，代码的可复用性（然而并用不到）提高了

* 数据文件和输出文件也更加规范了

* 输出的数据更多了（然后为此做到头都大了）

大概就是这些吧，具体的内容如下，然后再重构一下代码

## 0311更新

将csv存储修改为SQLite存储

        """CREATE TABLE returns
            (
            ID int  identity (1,1) ,
            StockID varchar(20),
            LongFac float,
            ShortFac float,
            LongMA int,
            ShortMA int,
            StartYear int,
            EndYear int,
            Return float,
            PRIMARY KEY(ID)
            );
        """

emmmm，说起来就是好几个循环，所以如果要设置主键的话有点多，就直接令了一个ID做主键了