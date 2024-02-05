export const orderingMethods = {
    addOrdering(newOrdering){
        if (this.ordering == newOrdering){
          let paramName = newOrdering.slice(newOrdering.indexOf("=") + 1,);
          this.ordering = this.ordering.slice(0, this.ordering.indexOf("=") + 1) + "-" + paramName;
        } else {
          this.ordering = newOrdering
        };
        this.pageUrl = this.cleanUrl + this.params + this.ordering ;
        this.loadElements();
      },

      changeParams(param) {
        let paramName = param.slice(0, param.indexOf("=") + 1);
        if (!this.params.includes(paramName)) {
          this.params = this.params + param;
        } else {
          this.params = this.params.replace(new RegExp(paramName + "[^&]*" + "&"), param );
        };
        this.pageUrl = this.cleanUrl + this.params;
        this.loadElements();
      },

      loadElements(){
        axios.get(this.pageUrl).then(
          response =>{
            console.log(response.data)
            this.elements = response.data.results;
            this.paginationInfo = {
              currentPage: response.data.current_page,
              totalPages: response.data.pages,
              totatElements: response.data.count
            };
            this.pageUrl = response.data.next;
            } 
            ).catch(error =>{
                  if (error.response) {
                    console.log(error.response.data)
                  }
                  })
      },

      clearFilters(){
        this.params = '';
        this.ordering = '';
        this.filteredRegistryType = '',
        this.filteredRegistryStatus = '',
        this.pageUrl = this.cleanUrl;
        this.loadElements();
      },


      loadNextPage() {
        const nextPage = parseInt(this.paginationInfo.currentPage) + 1;
        this.pageUrl = this.cleanUrl + "page=" + nextPage + "&" + this.params + this.ordering;
        this.loadElements();
      },
      loadPreviousPage() {
        const previousPage = parseInt(this.paginationInfo.currentPage) - 1;
        this.pageUrl = this.cleanUrl + "page=" + previousPage + "&" + this.params + this.ordering;
        this.loadElements();
      },
  
      loadRequestedPage(page) {
        this.pageUrl = this.cleanUrl + "page=" + page + "&" + this.params + this.ordering;
        this.loadElements();
    
      },
      generatePagesRange(currentPage, totalPages, gap) {
        const range = [];
        currentPage = parseInt(currentPage)
        let start = Math.max(0, currentPage - gap - 1);
        let end = Math.min(currentPage + gap, totalPages);
        for (let i = start; i <= end - 1; i++) {
          range.push(i);
        }
        return range;
      },

      showingElems(){
        if (this.paginationInfo.totatElements){ 
        let start = (this.paginationInfo.currentPage - 1)*10 + 1;
        let end = Math.min(this.paginationInfo.currentPage*10, this.paginationInfo.totatElements);
        return `${start} - ${end}`}
        else return 0
      },
  };