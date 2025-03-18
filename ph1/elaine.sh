buildurls () {

python buildurls.py

}

geturls () {

python geturls.py

}

transcripts () {

ls html_talks | sed 's/.html//' > files

while read file
do
  echo "--- extracting txt talk txt/"$file".txt ---"
  tr -d '~' < html_talks/"$file".html | tr '/' '~' > z
  sed -nE '/<!-- Transcript text -->/,/<!-- ~Transcript text -->/p' z | tr '\t' ' ' | tr -s ' ' | tr '~' '/' | html2text > txt/"$file".txt
done < files

}

metadata () {

rm -f metadata/*

ls html_talks | sed 's/.html//' > files

while read file
do
  echo "---- metadata for $file ----"
  tr '{}' '\n' < html_talks/"$file".html | grep -m1 '"tag"' | sed 's/,"/~/g' | tr '~' '\n' > o

  tedid=$( grep '"id"' o | cut -d':' -f2 | tr -dc '0-9' )
#  tags=$( grep '^tag"' o | cut -d':' -f2 | tr ',' '\n' | tr -d '"' | tr '[A-Z]' '[a-z]' )
  tags=$( grep '^tag"' o | cut -d':' -f2  | tr -d '"' | tr '[A-Z]' '[a-z]' )
  year=$( grep '^year"' o | cut -d':' -f2 | tr -dc '0-9' | tr -d '"' )
  event=$( grep '^event"' o | cut -d':' -f2 | tr -d '"' )
  talk=$( grep '^talk"' o | cut -d':' -f2 | tr -d '"' )
  views=$( grep -B1 'views</span' html_talks/"$file".html | head -1 | tr -dc '[0-9]\n' )
  video=$( tr '{}' '\n' < html_talks/"$file".html | grep -m1 '"bitrate"' | tr '"' '\n' | grep https | sed 's/?dnt//' )
  speaker=$( tr '{}' '\n' < html_talks/"$file".html | grep -m1 '"speaker"' | tr '"' '\n' | grep -A2 '^speaker' | grep -v -e 'speaker' -e ':' )
  title=$( tr '{}' '\n' < html_talks/"$file".html | grep -m1 '"title"' | tr '"' '\n' | grep -A2 '^title' | grep ':' | cut -d':' -f2 | sed 's/^[ ]*//' )
  duration=$( tr '{}' '\n' < html_talks/"$file".html | grep -m1 '"duration"' | tr '"' '\n' | grep -A2 '^duration' | grep ':' | cut -d':' -f2 | tr -dc '[0-9.]' | sed 's/^[ ]*//' )
 
  echo "$file	$tedid" | sed 's/	$/	NODATA/' >> metadata/ted_id.tab
  echo "$file	$tags" | sed 's/	$/	NODATA/'>> metadata/tags.tab
  echo "$file	$year" | sed 's/	$/	NODATA/'>> metadata/year.tab
  echo "$file	$event" | sed 's/	$/	NODATA/'>> metadata/event.tab
  echo "$file	$talk" | sed 's/	$/	NODATA/'>> metadata/talk.tab
  echo "$file	$views" | sed 's/	$/	NODATA/'>> metadata/views.tab
  echo "$file	$video" | sed 's/	$/	NODATA/'>> metadata/video.tab
  echo "$file	$speaker" | sed 's/	$/	NODATA/'>> metadata/speaker.tab
  echo "$file	$title" | sed 's/	$/	NODATA/'>> metadata/title.tab
  echo "$file	$duration" | sed 's/	$/	NODATA/'>> metadata/duration.tab

done < files

cat valid_urls > metadata/links.tab

wc -w txt/* | grep txt | sed -e 's;txt/;;' -e 's;.txt;;' -e 's/^[ ]*//' -e 's/\(.*\) \(.*\)/\2 \1/' | tr ' ' '\t' > metadata/wordcount.tab

}

spreadsheet () {

echo "file_id	link	speaker	wordcount	title	duration	tags	views	year	talk	video	event	ted_id" > spreadsheet_elaine.tab

paste metadata/links.tab metadata/speaker.tab metadata/wordcount.tab metadata/title.tab metadata/duration.tab metadata/tags.tab metadata/views.tab metadata/year.tab metadata/talk.tab metadata/video.tab metadata/event.tab metadata/ted_id.tab | cut -f1,2,4,6,8,10,12,14,16,18,20,22,24 >> spreadsheet_elaine.tab

}

#buildurls
geturls
#transcripts
#metadata
#spreadsheet