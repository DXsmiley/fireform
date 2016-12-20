# Used to profile a fireform project
#
# arguments:
#  1. name of project (required)
#  2. output sort order (optional, see cookbook for possible values)
#
# All output is piped to profile.txt

sort_by="time"
if [ "$2" != "" ]; then
	sort_by="$2"
fi

filename="./$1/__main__.py"

python -m cProfile -s $sort_by $filename > profile.txt
