if [ -d "terraform.tfstate.d/$1" ]; then 
  terraform workspace select $1
else
  terraform workspace new $1
fi

python3 render.py $1

terraform apply -var="topic=$1" -var="bucket=$2"
