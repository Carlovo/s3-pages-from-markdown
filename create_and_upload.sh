id="${1}-${2}"
if [ -d "terraform.tfstate.d/$id" ]; then
  terraform workspace select $id
else
  terraform workspace new $id
fi

python3 render.py $1 $2

terraform apply -var="topic=$1" -var="bucket=$2"
