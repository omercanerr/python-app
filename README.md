# Kubernetes installation with kubeadm

cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter


cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF


sudo sysctl --system

sudo swapoff -a
(crontab -l 2>/dev/null; echo "@reboot /sbin/swapoff -a") | crontab - || true

sudo apt-get update -y
sudo apt-get install -y software-properties-common curl apt-transport-https ca-certificates

curl -fsSL https://pkgs.k8s.io/addons:/cri-o:/prerelease:/main/deb/Release.key |
    gpg --dearmor -o /etc/apt/keyrings/cri-o-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/cri-o-apt-keyring.gpg] https://pkgs.k8s.io/addons:/cri-o:/prerelease:/main/deb/ /" |
    tee /etc/apt/sources.list.d/cri-o.list

sudo apt-get update -y
sudo apt-get install -y cri-o

sudo systemctl daemon-reload
sudo systemctl enable crio --now
sudo systemctl start crio.service

VERSION="v1.28.0"
wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
sudo tar zxvf crictl-$VERSION-linux-amd64.tar.gz -C /usr/local/bin
rm -f crictl-$VERSION-linux-amd64.tar.gz


KUBERNETES_VERSION=1.29

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v$KUBERNETES_VERSION/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v$KUBERNETES_VERSION/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list


sudo apt-get update -y

apt-cache madison kubeadm | tac

# only master
sudo apt-get install -y kubelet=1.29.0-1.1 kubectl=1.29.0-1.1 kubeadm=1.29.0-1.1
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
POD_CIDR="192.168.0.0/16"
sudo kubeadm init --apiserver-advertise-address=192.168.0.37  --apiserver-cert-extra-sans=192.168.0.37  --pod-network-cidr=$POD_CIDR --node-name master --ignore-preflight-errors Swap
kubeadm token create --print-join-command

kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# only worker
sudo apt-get install -y kubelet=1.29.0-1.1 kubeadm=1.29.0-1.1
sudo apt-get install -y kubelet kubeadm
sudo apt-mark hold kubelet kubeadm

## After creating Kubernetes for worker, you should recreate each 24 hours. If you want to add node! At same for master!
kubeadm join 192.168.0.37:6443 --token rt50qm.cve3saz1yitww178 --discovery-token-ca-cert-hash sha256:ff55c3f1f86ee435ed70143ac9f586a95c769408c939c97ff51629

---
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
---



# Kubernetes conver installation for creating deploy.yaml k8s

curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose

snap install kompose

# Prometheous

kubectl create namespace monitoring
kubectl apply -f prometheous.yaml

# JENKINS INSTALLATION

sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins

# Installation of Java

sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version
openjdk version "17.0.10" 2024-01-16
OpenJDK Runtime Environment (build 17.0.8+7-Debian-1deb12u1)
OpenJDK 64-Bit Server VM (build 17.0.8+7-Debian-1deb12u1, mixed mode, sharing)

sudo systemctl enable jenkins

sudo systemctl start jenkins

sudo systemctl status jenkins

 cat /var/lib/jenkins/secrets/initialAdminPassword
 jenkins    10833 20.4 32.4 3146112 652292 ?      Ssl  00:57   0:36 /usr/bin/java -Djava.awt.headless=true -jar /usr/share/java/jenkins.war --webroot=/var/cache/jenkins/war --httpPort=8080

## KAYNAK
https://pypi.org/project/prometheus-flask-exporter/
https://www.jenkins.io/doc/book/installing/linux/#prerequisites
https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/