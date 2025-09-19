import sys
import volcdb

# Get the frame value from the command line
# sys.argv[0] is the script name, sys.argv[1] is the first argument
if len(sys.argv) != 2:
    print("Usage: python frame2listavolcanes.py <frame>")
    sys.exit(1)

frame = sys.argv[1]

# Call volcdb with the frame variable
volcanoes = volcdb.get_volcanoes_in_frame(frame)

# Print the results
print(volcanoes)
