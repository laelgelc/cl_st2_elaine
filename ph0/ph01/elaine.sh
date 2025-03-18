buildurls () {

grep "<a class=' ga-link' data-ga-context='talks'" indexes/*.html | sort | uniq | cut -d'/' -f3-  > z

while read u
do
  count=$( echo $u | tr -dc '_' | wc -c )
  echo $count	$u
done < z > zz

grep -v '^1 ' zz | cut -d' ' -f2- | sed -e "s/'>//" -e "s;\(.*\);https://www.ted.com/\1/transcript?language=en;" | nl -nrz > valid_urls

}

geturls () {

python geturls.py

}

#buildurls
#geturls
