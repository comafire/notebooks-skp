var index = new Vue({
  el: '#Index',
  data: {
    files: [],
    completed: 0,
    status: false,
    dnnPredClass: 0,
    dnnPredProb: 0.0,
    cnnPredClass: 0,
    cnnPredProb: 0.0,      
    id: '',
    pw: '',
    level: "A",
    id: '',
    accessToken: '',
    refreshToekn: ''
  },
  created () {

  },
  methods: {
    signIn () {
      axios({
        url: "/skp/v1/tokens",
        method: "post",
        data: {
          'id' : this.id,
          'pw' : this.pw,
          'level' : this.level
        }
      })
      .then((response) => {
        var data = response['data'];
        console.log(response);
        this.accessToken = data['access_token'];
        this.refershToken = data['refresh_token'];
      })
      .catch((response) => {
        console.log(response);
      });
    },     
    setUploadFiles() {
      console.log("setUploadFiles()")
      console.log(this.$refs.uploadFiles.files)
      this.files = this.$refs.uploadFiles.files
      this.getImagePreviews()
    },
    getImagePreviews() {
      for( let i = 0; i < this.files.length; i++ ){
        if ( /\.(jpe?g|png|gif)$/i.test( this.files[i].name ) ) {
          let reader = new FileReader();
          reader.addEventListener("load", function(){
            this.$refs['image'+parseInt( i )][0].src = reader.result;
          }.bind(this), false);
          reader.readAsDataURL( this.files[i] );
        }
      }
    },
    submitFiles(){
      this.completed = 0;
      this.status = false;
      for( var i = 0; i < this.files.length; i++ ){
        let formData = new FormData();
        formData.append('file', this.files[i]);

        axios({
          url: "/mnist/v1/dnn",
          method: "post",
          headers: {
            'Authorization' : "Bearer " + this.accessToken,
            'Content-Type': 'multipart/form-data'
          },
          data: formData
        })
        .then((response) => {
          var data = response['data'];
          console.log("submitFiles: SUCCESS");
          console.log(response);
          this.completed++;
          if (this.completed === this.files.length) {
            this.status = true;
          }
          this.dnnPredClass = data['pred_class']
          this.dnnPredProb = data['pred_prob']
        })
        .catch((response) => {
          console.log("submitFiles: FAIL");
          console.log(response);
        });

        axios({
          url: "/mnist/v1/cnn",
          method: "post",
          headers: {
            'Authorization' : "Bearer " + this.accessToken,
            'Content-Type': 'multipart/form-data'
          },
          data: formData
        })
        .then((response) => {
          var data = response['data'];
          console.log("submitFiles: SUCCESS");
          console.log(response);
          this.completed++;
          if (this.completed === this.files.length) {
            this.status = true;
          }
          this.cnnPredClass = data['pred_class']
          this.cnnPredProb = data['pred_prob']
        })
        .catch((response) => {
          console.log("submitFiles: FAIL");
          console.log(response);
        });
          
      }
    }
  }
});
