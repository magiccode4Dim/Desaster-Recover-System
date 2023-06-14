# DRS
DDoS Resilience System
- Este Sistema possibita que um administrador de Sistemas crie um redundância do seu sistema original em uma rede Kubernets sem que seja necessário alterar a aplicação;
- Após criar a redundância, uma aplicação cliente será instalada no servidor do administrador de Sistemas;
- A aplicação clientes vai fazer a monitoria e os backups da base de dados da aplicação do Administrador de redes para manter a instância actualizada;
- No caso do servidor interno do Administrador de Sistemas receber uma sobrecarga(Um ataque DDoS ou aumento de Demanda) que potêncialmente poderá fazer o servidor interno parar;
- Uma instância da rede Kubernets deste Sistema será criada e o trafego do servidor do administrador de Sistemas passará a ser encaminhado para a rede Kubernets;
- A rede Kubernes Fará o Balanceamneto de Carga entre os POTS para que possa suprir a demanda gerado no servidor do  administrador de sistemas.
- Fazendo assim com que o aplicativo Web permaneça online mesmo em caso de ataque ou aumento de demanda. 
