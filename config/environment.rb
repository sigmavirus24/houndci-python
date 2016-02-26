$LOAD_PATH.unshift(".", "lib")

# require "config/initializers/dotenv"

$stdout.sync = true

# Dir.glob("config/initializers/**/*.rb").each { |file| require file }
Dir.glob("lib/**/*.rb").each { |file| require file }
