this_path=$(cd `dirname $0`;pwd)

cd $this_path
echo $this_path
current_date=`date -d "-1 day" "+%Y%m%d"`
echo $current_date
split -b 1048576000 -d -a 3 log/nohup.out log/log_${current_date}_

cat /dev/null > nohup.out
