import os, sys
libdir = os.path.join(os.path.dirname(__file__), '..')
if libdir[-1] != os.path.sep:
    libdir += os.path.sep
sys.path.insert(0, libdir)
import pycdio
import cdio
import musicbrainzngs
from libdiscid import read

musicbrainzngs.set_useragent("bunkerripper", "INDEV", "https://github.com/idotmaster1/bunkerripper")

# Define the audio cd
if sys.argv[1:]:
    try:
        cd = cdio.Device(sys.argv[1])
    except IOError:
        print("Problem opening CD-ROM: %s" % sys.argv[1])
        sys.exit(1)
else:
    try:
        cd = cdio.Device(driver_id=pycdio.DRIVER_UNKNOWN)
    except IOError:
        print("Problem finding a CD-ROM")
        sys.exit(1)

# Get first track from CD-ROM
firsttrack = cd.get_first_track()
if firsttrack is None:
    print("Error getting first track from CD-ROM")
    sys.exit(2)

first_track = firsttrack.track
num_tracks  = cd.get_num_tracks()
last_track  = first_track+num_tracks-1

print("First track: %s" % first_track)
print("Number of tracks: %s" % num_tracks)
print("Last track: %s" % last_track)

# Run an ffmpeg command to start ripping the CD
# Im not using this rn because im too lazy to make it work: os.system('sh rip.sh ' + str(num_tracks))
#os.system("cdparanoia -XB")

# Get disc id
disc = read(features=0)
print(disc.id)

# Get data with the discid
turnnumberintocomputernumber = last_track - 1
result = musicbrainzngs.get_releases_by_discid(disc.id, includes=["artists", "recordings"])
t = (result["disc"]["release-list"][0]["medium-list"][0]["track-list"])
print(t)
for x in range(len(t)):
    line = (t[x])
    print(f'{line["number"]}. {line["recording"]["title"]}')

