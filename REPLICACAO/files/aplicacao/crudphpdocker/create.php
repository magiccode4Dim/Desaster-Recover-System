<?php
require 'includes/header.php';

if (isset($_POST['tambah'])) {
    if (insert($_POST) == 1) {
        return header('Location: index.php');
    } else {
        return "error";
    }
}
?>

<div class="container my-4">
    <div class="row">
        <div class="col col-4 mx-auto">
            <div class="card shadow">
                <div class="card-header">
                    <h4 class="text-center">Inserir Cor</h4>
                </div>
                <div class="card-body">
                    <form action="" method="post">
                        <div class="form-group">
                            <label for="">ID</label>
                            <input type="text" name="id" class="form-control">
                        </div>
                        <div class="form-group">
                            <label for="">Cor</label>
                            <input type="text" name="cor" class="form-control">
                        </div>
                        <div class="form-group">
                            <label for="">Data</label>
                            <input type="text" name="data" class="form-control">
                        </div>
                        <div class="form-group">
                            <label for="">Dono</label>
                            <input type="text" name="dono" class="form-control">
                        </div>
                </div>
                <div class="card-footer">
                    <div class="d-flex justify-content-around">
                        <a href="index.php" class="btn btn-danger btn-sm">Voltar</a>
                        <button type="submit" name="tambah" class="btn btn-primary btn-sm">Inserir</button>
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
