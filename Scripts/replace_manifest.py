import requests, argparse, json, time

# Setup arguments
parser = argparse.ArgumentParser(description='Replace value in manifest file') 
parser.add_argument('-manifest','-m', action="store", dest="manifest_file", help='Manifest JSON File in current dir e.g. manifest.json')
parser.add_argument('-propvalue','-v', action="store", dest="property_value", help='Value to replace property')

args = parser.parse_args()

def replace_values(manifest,  value):
    print("starting rest loop")

    data = read_json_file(manifest)
    data['environment']['deployment']['packageId'] = value
    write_json_file(manifest, data)
    #print(data)

def read_json_file(filename):
    with open(filename,'r') as f:
        print('Reading from file...')
        data = json.load(f)
        return data

def write_json_file(file, data):
    with open(file, 'w') as f:
        print('Writing to file...')
        json.dump(data, f)
        print('Done writing....')
##
##	Main execution 
##
def main():
    print("Main execution started")
    replace_values(args.manifest_file,  args.property_value)


if __name__ == "__main__":
    main()