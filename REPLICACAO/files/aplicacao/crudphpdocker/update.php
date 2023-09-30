<?php
require 'includes/header.php';

if (isset($_GET['id'])) {
    $data = getById($_GET['id']);
}

if (isset($_POST['update'])) {
    var_dump($_POST);
    $update = update($_POST);
    if ($update == 1) {
        return header('Location: index.php');
    }
}

?>

<div class="container my-4">
    <div class="row">
        <div class="col col-4 mx-auto">
            <div class="card shadow">
                <div class="card-header">
                    <h4 class="text-center">Actualizar Cor</h4>
                </div>
                <div class="card-body">
                    <form action="" method="post">
                        <input type="hidden" name="mine_id" value="<?= $data['mine_id'] ?>">
                        <div class="form-group">
                            <label for="">ID</label>
                            <input type="text" name="id" class="form-control" value="<?= $data['id'] ?>">
                        </div>
                        <div class="form-group">
                            <label for="">Cor</label>
                            <input type="text" name="cor" class="form-control" value="<?= $data['cor'] ?>">
                        </div>
                        <div class="form-group">
                            <label for="">Data</label>
                            <input type="text" name="data" class="form-control " value="<?= $data['data'] ?>">
                        </div>
                        <div class="form-group">
                            <label for="">Dono</label>
                            <input type="text" name="dono" class="form-control" value="<?= $data['dono'] ?>">
                        </div>
                </div>
                <div class="card-footer">
                    <div class="d-flex justify-content-around">
                        <a href="index.php" class="btn btn-danger btn-sm">Voltar</a>
                        <button type="submit" name="update" class="btn btn-primary btn-sm">Update</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php
require 'includes/footer.php';
?>
