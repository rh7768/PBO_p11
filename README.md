Refactoring Sistem Validasi Registrasi Mahasiswa dilakukan untuk memperbaiki struktur kode agar sesuai dengan prinsip SOLID. Pada kode awal, seluruh proses validasi SKS dan prasyarat dilakukan dalam satu class menggunakan kondisi if/else, sehingga melanggar prinsip Single Responsibility Principle (SRP), Open/Closed Principle (OCP), dan Dependency Inversion Principle (DIP).

Pelanggaran SRP terjadi karena satu class menangani lebih dari satu tanggung jawab, sedangkan pelanggaran OCP muncul karena penambahan aturan validasi baru mengharuskan perubahan pada kode yang sudah ada. Selain itu, kode awal juga melanggar DIP karena class utama bergantung langsung pada detail aturan validasi tanpa menggunakan abstraction.

Refactoring dilakukan dengan menerapkan interface Validator sebagai abstraction dan memisahkan setiap jenis validasi ke dalam class tersendiri. Class ValidatorManager hanya bergantung pada abstraction dan bertugas mengatur alur validasi, sehingga sistem dapat dikembangkan tanpa mengubah kode lama.

Setelah refactoring, setiap class memiliki satu tanggung jawab yang jelas. Pemisahan ini membuat kode lebih modular, fleksibel, mudah dikembangkan, dan sesuai dengan konsep pemrograman berorientasi objek.
